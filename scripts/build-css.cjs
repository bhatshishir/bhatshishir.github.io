const fs = require('fs');
const postcss = require('postcss');
const config = require('../postcss.config.js');
const input = 'assets/css/tailwind.css';
const output = 'assets/css/style.css';
postcss(config.plugins).process(fs.readFileSync(input, 'utf8'), { from: input, to: output }).then(result => {
  fs.writeFileSync(output, result.css);
  result.warnings().forEach(warning => console.warn(warning.toString()));
  console.log(`Built ${output} (${result.css.length} bytes)`);
}).catch(error => { console.error(error); process.exit(1); });
