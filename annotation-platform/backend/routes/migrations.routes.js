const { authJwt } = require("../middleware");
const controller = require("../controllers/migrations.controller");

module.exports = function(app) {
  app.use(function(req, res, next) {
    res.header(
      "Access-Control-Allow-Headers",
      "x-access-token, Origin, Content-Type, Accept"
    );
    next();
  });

  app.get("/api/migrations/batch", [authJwt.verifyToken, authJwt.isAdmin] ,controller.migrateBatch);
};
