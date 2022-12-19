'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class Screening extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
      Screening.belongsTo(models.User, {
        foreignKey: "annotatorId",
        as: "annotators"
      });

      Screening.belongsTo(models.Meme, {
        foreignKey: "memeId",
        as: "memes"
      });

      Screening.belongsToMany(models.Tag, {
        through: "ScreeningTag",
        foreignKey: "screeningId",
        otherKey: "tagId",
        as: "tags"
      });

      Screening.belongsToMany(models.Pillar, {
        through: "ScreeningPillar",
        foreignKey: "screeningId",
        otherKey: "pillarId"
      });
      
      Screening.hasMany(models.ScreeningPillar, {
        foreignKey: "screeningId",
        as: "pillars"
      });
    }
  }
  Screening.init({
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    annotatorId: {
      type: DataTypes.INTEGER,
      unique: "annotatorMeme"
    },
    memeId: {
      type: DataTypes.INTEGER,
      unique: "annotatorMeme"
    },
    text: DataTypes.STRING,
    contentType: DataTypes.INTEGER,
    relatedCountry: DataTypes.INTEGER,
    flagged: DataTypes.INTEGER
  }, {
    sequelize,
    modelName: 'Screening',
  });
  return Screening;
};