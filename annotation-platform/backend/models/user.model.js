'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class User extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
      User.belongsToMany(models.Role, {
        through: "UserRoles",
        foreignKey: "userId",
        otherKey: "roleId"
      });

      User.hasMany(models.Screening, { 
        foreignKey: "annotatorId",
        as: "screenings" 
      });

      User.belongsToMany(models.Batch, {
        through: "UserBatch",
        foreignKey: "userId",
        otherKey: "batchId",
        as: "batches"
      });
    }
  };
  User.init({
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    username: DataTypes.STRING,
    password: DataTypes.STRING,
    updatePassword: DataTypes.INTEGER
  }, {
    sequelize,
    modelName: 'User',
  });
  return User;
};