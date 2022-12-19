'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class Tag extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here

      Tag.belongsToMany(models.Screening, {
        through: "ScreeningTag",
        foreignKey: "tagId",
        otherKey: "screeningId"
      });

      Tag.belongsTo(models.User, {
        foreignKey: "annotatorId",
        as: "annotator"
      });
    }
  }
  Tag.init({
    id: {
      allowNull: false,
      autoIncrement: true,
      primaryKey: true,
      type: DataTypes.INTEGER
    },
    name: {
      type: DataTypes.STRING,
    },
    annotatorId: {
      type: DataTypes.INTEGER,
    }
  }, {
    sequelize,
    modelName: 'Tag',
  });
  return Tag;
};