const path = require("path");

// DB Configuration for other dialects (e.g. MySQL and etc)
// module.exports = {
//   HOST: "localhost",
//   USER: "root",
//   PASSWORD: "123456",
//   DB: "testdb",
//   dialect: "mysql",
//   pool: {
//     max: 5,
//     min: 0,
//     acquire: 30000,
//     idle: 10000
//   }
// };

// DB Configuration for SQLite
var development = {
  "username": "root",
  "password": "password",
  "storage": path.join(__dirname, '..', 'database_dev.sqlite3'),
  "host": "localhost",
  "dialect": "sqlite",
}

var production = {
  "username": "root",
  "password": "password",
  "storage": path.join(__dirname, '..', 'database_prod.sqlite3'),
  "host": "localhost",
  "dialect": "sqlite"
}

module.exports = {
  "development": development,
  "production": production,
};