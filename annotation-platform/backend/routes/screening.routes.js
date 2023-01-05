const { authJwt } = require("../middleware");
const controller = require("../controllers/screening.controller");

module.exports = function(app) {
  app.use(function(req, res, next) {
    res.header(
      "Access-Control-Allow-Headers",
      "x-access-token, Origin, Content-Type, Accept"
    );
    next();
  });

  app.post("/api/screening/create", [authJwt.verifyToken, authJwt.isAdmin], controller.create);
  app.post("/api/screening/review", [authJwt.verifyToken, authJwt.isAnnotator], controller.review);
  app.put("/api/screening/:screeningId", [authJwt.verifyToken, authJwt.isAnnotator], controller.update);
  app.get("/api/screening/:batchId", [authJwt.verifyToken, authJwt.isAnnotator], controller.fetch);
  app.get("/api/screening", [authJwt.verifyToken, authJwt.isAnnotator], controller.fetchAll);

  app.get("/api/report/:batchId", [authJwt.verifyToken, authJwt.isAdmin], controller.generate);
};
