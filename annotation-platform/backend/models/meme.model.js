'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class Meme extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // // define association here
      // Meme.belongsTo(models.Batch, {
      //   foreignKey: "batchId"
      // });

      Meme.belongsToMany(models.Batch, {
        through: models.MemeBatch,
        foreignKey: "memeId",
        otherKey: "batchId",
        as: "batches"
      });

      Meme.hasMany(models.Screening, { 
        foreignKey: "memeId",
        as: "screenings" 
      });
    }
  };
  Meme.init({
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    filename: {
      allowNull: false,
      unique: true,
      type: DataTypes.STRING
    },
    text: DataTypes.STRING,
    platform: DataTypes.STRING,
    source: DataTypes.STRING,
    keywords: DataTypes.STRING,
    priority: DataTypes.STRING,
    batchId: DataTypes.INTEGER,
  }, {
    sequelize,
    modelName: 'Meme',
  });
  return Meme;
};