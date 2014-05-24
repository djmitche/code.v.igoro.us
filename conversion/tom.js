var toMarkdown = require('to-markdown').toMarkdown;
var fs = require('fs');
fs.readFile('codevigorous.html', 'utf8', function(err, data) {
    console.log(toMarkdown(data));
});
