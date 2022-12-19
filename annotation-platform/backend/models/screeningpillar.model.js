'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class ScreeningPillar extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
      
      ScreeningPillar.belongsTo(models.Screening, {
        foreignKey: "screeningId"
      });
      
      ScreeningPillar.belongsTo(models.Pillar, {
        foreignKey: "pillarId"
      });
    }
  }
  ScreeningPillar.init({
    screeningId: DataTypes.INTEGER,
    pillarId: DataTypes.INTEGER,
    stance: DataTypes.STRING
  }, {
    sequelize,
    modelName: 'ScreeningPillar',
    timestamps: false
  });
  return ScreeningPillar;
};