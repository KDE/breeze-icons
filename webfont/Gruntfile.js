module.exports = function(grunt) {
    'use strict';

    grunt.initConfig({
        // Create the webfont files:
        webfont: {
                icons: {
                        src: '../icons/actions/22@2x/*.svg',
                        dest: './dist',
                        options: {
                            stylesheet: 'css',
                            types:  'eot,woff2,ttf,svg',
                            optimize: false
                        }
                }
        }
    });
    grunt.loadNpmTasks('grunt-webfont');
    
    // Run the default task by executing "grunt" in the CLI:
    grunt.registerTask('default', ['webfont']);
};

