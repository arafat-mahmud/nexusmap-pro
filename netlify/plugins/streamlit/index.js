const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

module.exports = {
  onPreBuild: async ({ utils }) => {
    console.log('Installing Python and dependencies...');
    
    // Ensure Python 3.9 is available
    try {
      // Create directories if they don't exist
      if (!fs.existsSync(path.join(process.cwd(), 'output'))) {
        fs.mkdirSync(path.join(process.cwd(), 'output'));
      }
      
      if (!fs.existsSync(path.join(process.cwd(), 'templates'))) {
        fs.mkdirSync(path.join(process.cwd(), 'templates'));
      }
      
      // Install Python dependencies
      await utils.run.command('pip install -r requirements.txt');
      console.log('Successfully installed Python dependencies');
    } catch (error) {
      utils.build.failBuild('Failed to install Python dependencies', { error });
    }
  }
};
