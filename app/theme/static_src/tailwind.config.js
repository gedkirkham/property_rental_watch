
const colors = require('tailwindcss/colors')

module.exports = {
    purge: {
        enabled: process.env.NODE_ENV === 'production',
        content: [
            '../../templates/*.html', // base templates
            '../../**/templates/**/*.html', // app specific templates
        ]
    },
    prefix: 'tw-',
    variants: {},
    plugins: [],
    theme: {
        colors: {
            white: '#fff',
            black: '#000',
            
            blueGray: colors.blueGray,
            coolGray: colors.coolGray,
            gray: colors.gray,
            trueGray: colors.trueGray,
            warmGray: colors.warmGray,
            red: colors.red,
            orange: colors.orange,
            amber: colors.amber,
            yellow: colors.yellow,
            lime: colors.lime,
            green: colors.green,
            emerald: colors.emerald,
            teal: colors.teal,
            cyan: colors.cyan,
            lightBlue: colors.lightBlue,
            blue: colors.blue,
            indigo: colors.indigo,
            violet: colors.violet,
            purple: colors.purple,
            fuchsia: colors.fuchsia,
            pink: colors.pink,
            rose: colors.rose,
        }
    }
}