'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class Pillar extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
      Pillar.belongsToMany(models.Screening, {
        through: "ScreeningPillar",
        foreignKey: "pillarId",
        otherKey: "screeningId"
      });
    }
  }
  Pillar.init({
    name: DataTypes.STRING
  }, {
    sequelize,
    modelName: 'Pillar',
  });
  return Pillar;
};