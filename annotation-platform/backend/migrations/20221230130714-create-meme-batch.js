'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('MemeBatches', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      memeId: {
        type: Sequelize.INTEGER
      },
      batchId: {
        type: Sequelize.INTEGER
      },
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE
      }
    }).then(() => queryInterface.addIndex('MemeBatches', {
      fields: ['memeId', 'batchId'],
      unique: true
    }));
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('MemeBatches');
  }
};