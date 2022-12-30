'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class MemeBatch extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  MemeBatch.init({
    memeId: DataTypes.INTEGER,
    batchId: DataTypes.INTEGER
  }, {
    sequelize,
    modelName: 'MemeBatch',
  });
  return MemeBatch;
};