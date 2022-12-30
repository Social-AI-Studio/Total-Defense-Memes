'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class Batch extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
      Batch.belongsToMany(models.Meme, {
        through: models.MemeBatch,
        foreignKey: "batchId",
        otherKey: "memeId",
        as: 'memes'
      });

      Batch.belongsToMany(models.User, {
        through: "UserBatch",
        foreignKey: "batchId",
        otherKey: "userId"
      });
    }
  };
  Batch.init({
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true
    }
  }, {
    sequelize,
    modelName: 'Batch',
  });
  return Batch;
};