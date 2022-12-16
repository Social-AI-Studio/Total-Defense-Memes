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
module.exports = {
  HOST: "localhost",
  USER: "root",
  PASSWORD: "root",
  dialect: "sqlite",
  storage: path.join(__dirname, '..', 'database.sqlite')
};
