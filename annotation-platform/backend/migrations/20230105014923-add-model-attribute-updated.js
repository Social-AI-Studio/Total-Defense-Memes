'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    /**
     * Add altering commands here.
     *
     * Example:
     * await queryInterface.createTable('users', { id: Sequelize.INTEGER });
     */
    await queryInterface.addColumn(
      'screenings',
      'updated',
      {
        type: Sequelize.INTEGER,
        defaultValue: 0
      }
    )

    await queryInterface.addColumn(
      'screenings',
      'reviewed',
      {
        type: Sequelize.INTEGER,
        defaultValue: 1
      }
    )
  },

  async down(queryInterface, Sequelize) {
    /**
     * Add reverting commands here.
     *
     * Example:
     * await queryInterface.dropTable('users');
     */
    await queryInterface.removeColumn('screenings', 'updated')
    await queryInterface.removeColumn('screenings', 'reviewed')
  }
};
