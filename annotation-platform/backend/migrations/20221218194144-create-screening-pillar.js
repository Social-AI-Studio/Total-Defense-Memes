'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('ScreeningPillars', {
      screeningId: {
        allowNull: false,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      pillarId: {
        allowNull: false,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      stance: {
        allowNull: false,
        type: Sequelize.INTEGER
      }
    });
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('ScreeningPillars');
  }
};