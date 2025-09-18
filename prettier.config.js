/**
 * @see https://prettier.io/docs/configuration
 * @type {import("prettier").Config}
 */
const config = {
    overrides: [
        {
            files: "*.md",
            options: {
                proseWrap: "always",
            },
        },
    ],
};

module.exports = config;
