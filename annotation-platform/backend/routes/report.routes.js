const { authJwt } = require("../middleware");
const screeningController = require("../controllers/screening.controller");
const tagController = require("../controllers/tag.controller");

module.exports = function(app) {
  app.use(function(req, res, next) {
    res.header(
      "Access-Control-Allow-Headers",
      "x-access-token, Origin, Content-Type, Accept"
    );
    next();
  });

  app.get("/api/report/screening/:batchId", [authJwt.verifyToken, authJwt.isAdmin], screeningController.generate);
  app.get("/api/report/tag/:batchId", [authJwt.verifyToken, authJwt.isAdmin], tagController.generate);
};
