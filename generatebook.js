// node.js
const mume = require("@shd101wyy/mume");

async function main() {
  await mume.init();

  const engine = new mume.MarkdownEngine({
    filePath: "./docs/fullbook.md",
    config: {
      previewTheme: "github-light.css",
      // revealjsTheme: "white.css"
      codeBlockTheme: "default.css",
      breakOnSingleNewLine: false,
      printBackground: true,
      enableScriptExecution: true, // <= for running code chunks
    },
  });

  // html export
  await engine.htmlExport({ offline: false, runAllCodeChunks: true });
  console.log("Should be done.");

  // chrome (puppeteer) export
  await engine.chromeExport({ fileType: "pdf", runAllCodeChunks: true }); // fileType = 'pdf'|'png'|'jpeg'
  console.log("PDF export should be done.");

  return process.exit();
}

main();
