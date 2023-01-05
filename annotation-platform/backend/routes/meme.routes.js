const upload = require("../middleware/upload");
const controller = require("../controllers/meme.controller");

module.exports = function(app) {
  app.use(function(req, res, next) {
    res.header(
      "Access-Control-Allow-Headers",
      "x-access-token, Origin, Content-Type, Accept"
    );
    next();
  });

  app.post("/api/meme/upload", upload.single("file"), controller.addMemesToBatch);
};
