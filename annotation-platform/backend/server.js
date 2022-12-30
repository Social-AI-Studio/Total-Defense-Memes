const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();

global.__basedir = __dirname;

var corsOptions = {
	origin: [
		"http://localhost:8000",
		"https://tasks.mingshan.hee.com"
	]
};

app.use(cors(corsOptions));

// parse requests of content-type - application/json
app.use(bodyParser.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));

// database
const db = require("./models");

db.sequelize.sync();

// routes
require('./routes/auth.routes')(app);
require('./routes/meme.routes')(app);
require('./routes/screening.routes')(app);
require('./routes/tag.routes')(app);
require('./routes/migrations.routes')(app);

app.use('/img', express.static(__dirname + '/dataset/img'))

// set port, listen for requests
const HOST = process.env.HOST || '0.0.0.0'
const PORT = process.env.PORT || 8001

app.listen(PORT, HOST, () => {
	console.log(`Server is running on port ${PORT}.`);
});