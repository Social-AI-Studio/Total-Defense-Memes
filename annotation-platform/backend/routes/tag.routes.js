const controller = require("../controllers/tag.controller");

module.exports = function(app) {
  app.use(function(req, res, next) {
    res.header(
      "Access-Control-Allow-Headers",
      "x-access-token, Origin, Content-Type, Accept"
    );
    next();
  });

  app.post("/api/tag/create", controller.create);
  app.get("/api/tags",  controller.fetch);
};