---
layout: post
title:  "TIL about SSL certificate chains"
date:   2012-05-09 16:43:00
---


I'm
 laying some SSL groundwork for a project to allow puppet clients to
move between puppet servers without requiring a central CA, and without
requiring each client to be aware of all masters.  More on that in a
future post.

Based on ["Multiple Certificate Authorities"](http://projects.puppetlabs.com/projects/puppet/wiki/Multiple_Certificate_Authorities), I would like to have certificate chains that look like this:

          +-puppetmaster1 CA--+-puppetmaster1 server cert
          |                   |
          |                   +-client 1 server cert
    root--+                   :
          |
          +-puppetmaster2 CA--+-puppetmaster2 server cert
                              |
                              +-client 10 server cert
                              :

Then
all of the certificate validation would be done with the root CA
certificate as the trusted certificate.  A server certificate signed by
puppetmaster2's CA cert should then validate on puppetmaster1.

Building the certificates wasn't all that difficult - see [my comment on the bug](https://bugzilla.mozilla.org/show_bug.cgi?id=733110#c8)
 for the script.  However, while making sure the verification worked, I
ran into some non-obvious limitations of OpenSSL that are worth writing
down.

I began by running "openssl verify":

    [root@relabs-puptest1 ~]# openssl verify -verbose -CAfile puptest-certs/root-ca.crt -purpose sslclient puptest-certs/relabs08.build.mtv1.mozilla.com.crt
    puptest-certs/relabs08.build.mtv1.mozilla.com.crt: CN = relabs08.build.mtv1.mozilla.com, emailAddress = release@mozilla.com, O = "Mozilla, Inc.", OU = Release Engineering
    error 20 at 0 depth lookup:unable to get local issuer certificate

the
problem here is that the intermediate certificate is not available to
the verification tool.  Sources suggest to include it with the server
cert, by concatention, with the server cert last:

    cat puptest-certs/relabs-puptest1.build.mtv1.mozilla.com-ca.crt puptest-certs/relabs08.build.mtv1.mozilla.com.crt > relabs08-with-intermed.crt

However,
 after some struggle I learned that "openssl verify" does not recognize
this format -- it will only look at the first certificate in the file
(the intermediate), and if you don't look carefully you'll find that it
successfully verifies the intermediate, not the server certificate!
Sadly, s_client and s_sever don't support it either.  Apache httpd supports it with [SSLCACertificatePath](http://httpd.apache.org/docs/2.2/mod/mod_ssl.html#sslcacertificatepath).
  This will feed the certificate chain to the client, and also allow
httpd to verify client certificates without requiring the clients to
support an intermediate.

The Apache config is

    Listen 1443

    <VirtualHost *:1443>
            ServerName relabs-puptest1.build.mtv1.mozilla.com
            SSLEngine on
            SSLProtocol -ALL +SSLv3 +TLSv1
            SSLCipherSuite ALL:!ADH:RC4+RSA:+HIGH:+MEDIUM:-LOW:-SSLv2:-EXP

            SSLCertificateFile /etc/httpd/relabs-puptest1.build.mtv1.mozilla.com.crt
            SSLCertificateKeyFile /etc/httpd/relabs-puptest1.build.mtv1.mozilla.com.key
            SSLCACertificatePath /etc/httpd/ca-path

            # If Apache complains about invalid signatures on the CRL, you can try disabling
            # CRL checking by commenting the next line, but this is not recommended.
            #SSLCARevocationFile     /etc/puppet/ssl/ca/ca_crl.pem
            SSLVerifyClient require
            SSLVerifyDepth  2

    </VirtualHost>

While
 you're getting that set up, you're probably wondering where to get this
 fancy "c_rehash" utility.  Don't bother.  It's about as simple as:

    for i in *.crt; do
            h=`openssl x509 -hash -noout -in $i`
            rm -f $h.0
            ln -s $i $h.0
    done

As a side-note, the results of verification by s_client and s_server
 are not very obvious.  Look for the overall error message near the
bottom of the output.  Here's the result of a client verification once I
 had everything put together, with some long uselessness elided:

    [root@relabs-puptest1 ~]# openssl s_client -verify 2 -CAfile puptest-certs/root-ca.crt -cert puptest-certs/relabs08.build.mtv1.mozilla.com.crt -key puptest-certs/relabs08.build.mtv1.mozilla.com.key -pass pass:clientpass -connect localhost:1443
    verify depth is 2
    CONNECTED(00000003)
    depth=2 CN = PuppetAgain Root CA, emailAddress = release@mozilla.com, OU = Release Engineering, O = "Mozilla, Inc."
    verify return:1
    depth=1 CN = CA on relabs-puptest1.build.mtv1.mozilla.com, emailAddress = release@mozilla.com, O = "Mozilla, Inc.", OU = Release Engineering
    verify return:1
    depth=0 CN = relabs-puptest1.build.mtv1.mozilla.com, emailAddress = release@mozilla.com, O = "Mozilla, Inc.", OU = Release Engineering
    verify return:1
    ---
    Certificate chain
    0 s:/CN=relabs-puptest1.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    i:/CN=CA on relabs-puptest1.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    1 s:/CN=CA on relabs-puptest1.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    i:/CN=PuppetAgain Root CA/emailAddress=release@mozilla.com/OU=Release Engineering/O=Mozilla, Inc.
    2 s:/CN=PuppetAgain Root CA/emailAddress=release@mozilla.com/OU=Release Engineering/O=Mozilla, Inc.
    i:/CN=PuppetAgain Root CA/emailAddress=release@mozilla.com/OU=Release Engineering/O=Mozilla, Inc.
    ---
    Server certificate
    -----BEGIN CERTIFICATE-----
    MIIEeTCCA2GgAwIBAgIBATANBgkqhkiG9w0BAQUFADCBkTE1MDMGA1UEAxMsQ0Eg
    ...
    H90rZMVxsVyPHjjfXkeeFcSWyUnV/z3G9osrI9I9SaQ1o9bDc7ZheyHbWbhn
    -----END CERTIFICATE-----
    subject=/CN=relabs-puptest1.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    issuer=/CN=CA on relabs-puptest1.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    ---
    Acceptable client certificate CA names
    /CN=PuppetAgain Root CA/emailAddress=release@mozilla.com/OU=Release Engineering/O=Mozilla, Inc.
    /CN=CA on relabs-puptest1.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    /CN=CA on relabs-puptest2.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    ---
    SSL handshake has read 5379 bytes and written 1716 bytes
    ---
    ---
    New, TLSv1/SSLv3, Cipher is DHE-RSA-AES256-SHA
    Server public key is 2048 bit
    Secure Renegotiation IS supported
    Compression: zlib compression
    Expansion: zlib compression
    SSL-Session:
        Protocol  : TLSv1
        Cipher    : DHE-RSA-AES256-SHA
        Session-ID: E30634D9CFCC2FA327282DA813BB550C24ACDF18194E5F13C4981AA55914B5F0
        Session-ID-ctx:
        Master-Key: 013EB09B066418694D36D74B414BBA42E52DBF0066314B60FC7A74662A60934282B6C37C5C82026F70287E60F4FF9472
        Key-Arg   : None
        Krb5 Principal: None
        PSK identity: None
        PSK identity hint: None
        TLS session ticket:
        0000 - 82 5f 17 72 97 bd f3 1e-ec 24 de 69 ab 1e cd 1d   ._.r.....$.i....
        ....
        0520 - 40 05 b3 27 20 00 8d ce-93 a9 48 81 8f 0c 16 5b   @..' .....H....[

        Compression: 1 (zlib compression)
        Start Time: 1336582165
        Timeout   : 300 (sec)
        Verify return code: 0 (ok)
    ---

note the "Verify return code" at the bottom.

By way of demonstration that the server is actually checking those certs:

    [root@relabs-puptest1 ~]# openssl s_client -verify 2 -CAfile puptest-certs/root-ca.crt -cert bogus.crt -key bogus.key -pass pass:boguspass -connect localhost:1443
    verify depth is 2
    CONNECTED(00000003)
    depth=2 CN = PuppetAgain Root CA, emailAddress = release@mozilla.com, OU = Release Engineering, O = "Mozilla, Inc."
    verify return:1
    depth=1 CN = CA on relabs-puptest1.build.mtv1.mozilla.com, emailAddress = release@mozilla.com, O = "Mozilla, Inc.", OU = Release Engineering
    verify return:1
    depth=0 CN = relabs-puptest1.build.mtv1.mozilla.com, emailAddress = release@mozilla.com, O = "Mozilla, Inc.", OU = Release Engineering
    verify return:1
    140283463366472:error:14094418:SSL routines:SSL3_READ_BYTES:tlsv1 alert unknown ca:s3_pkt.c:1193:SSL alert number 48
    140283463366472:error:140790E5:SSL routines:SSL23_WRITE:ssl handshake failure:s23_lib.c:184:
    ---
    Certificate chain
    0 s:/CN=relabs-puptest1.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    i:/CN=CA on relabs-puptest1.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    1 s:/CN=CA on relabs-puptest1.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    i:/CN=PuppetAgain Root CA/emailAddress=release@mozilla.com/OU=Release Engineering/O=Mozilla, Inc.
    2 s:/CN=PuppetAgain Root CA/emailAddress=release@mozilla.com/OU=Release Engineering/O=Mozilla, Inc.
    i:/CN=PuppetAgain Root CA/emailAddress=release@mozilla.com/OU=Release Engineering/O=Mozilla, Inc.
    ---
    Server certificate
    -----BEGIN CERTIFICATE-----
    MIIEeTCCA2GgAwIBAgIBATANBgkqhkiG9w0BAQUFADCBkTE1MDMGA1UEAxMsQ0Eg
    ...
    H90rZMVxsVyPHjjfXkeeFcSWyUnV/z3G9osrI9I9SaQ1o9bDc7ZheyHbWbhn
    -----END CERTIFICATE-----
    subject=/CN=relabs-puptest1.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    issuer=/CN=CA on relabs-puptest1.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    ---
    Acceptable client certificate CA names
    /CN=PuppetAgain Root CA/emailAddress=release@mozilla.com/OU=Release Engineering/O=Mozilla, Inc.
    /CN=CA on relabs-puptest1.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    /CN=CA on relabs-puptest2.build.mtv1.mozilla.com/emailAddress=release@mozilla.com/O=Mozilla, Inc./OU=Release Engineering
    ---
    SSL handshake has read 3984 bytes and written 997 bytes
    ---
    New, TLSv1/SSLv3, Cipher is DHE-RSA-AES256-SHA
    Server public key is 2048 bit
    Secure Renegotiation IS supported
    Compression: zlib compression
    Expansion: NONE
    SSL-Session:
        Protocol  : TLSv1
        Cipher    : DHE-RSA-AES256-SHA
        Session-ID:
        Session-ID-ctx:
        Master-Key: 07E536F1C69A856857EA95DFD821BD6BBD499B5710642F9396D9525637EAD17C03064D5115B3D7F517EDE189E7AF40F8
        Key-Arg   : None
        Krb5 Principal: None
        PSK identity: None
        PSK identity hint: None
        Compression: 1 (zlib compression)
        Start Time: 1336582289    Timeout   : 300 (sec)
        Verify return code: 0 (ok)
    ---

Note the handshake failures near the top, where httpd closed the connection on the client.

The next step is to make CRLs work properly, since Puppet uses them extensively.

