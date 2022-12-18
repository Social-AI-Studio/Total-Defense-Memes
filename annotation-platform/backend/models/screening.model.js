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
        foreignKey: "annotatorId"
      });

      Screening.belongsTo(models.Meme, {
        foreignKey: "memeId"
      });
    }
  }
  Screening.init({
    annotatorId: {
      type: DataTypes.INTEGER,
      primaryKey: true
    },
    memeId: {
      type: DataTypes.INTEGER,
      primaryKey: true
    },
    contentType: DataTypes.INTEGER,
    relatedCountry: DataTypes.INTEGER,
    flagged: DataTypes.INTEGER
  }, {
    sequelize,
    modelName: 'Screening',
  });
  return Screening;
};