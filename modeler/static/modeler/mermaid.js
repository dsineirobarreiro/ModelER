import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.mjs';
import { saveFile } from './model.js';

mermaid.initialize({ startOnLoad: false });

const source_relations = {
    "Zero or One": "|o",
    "Exactly One": "||",
    "Zero or Many": "}o",
    "One or Many": "}|"
  };
  
  const target_relations = {
    "Zero or One": "o|",
    "Exactly One": "||",
    "Zero or Many": "o{",
    "One or Many": "|{"
  };
  
  function convert(data) {
    let merm = 'erDiagram\n';
    for (const ent of data.entities) {
      merm += `${ent.name} {\n`;
      merm += `  int ${ent.name}ID PK\n`;
      for (const attr of ent.attributes) {
        const name = attr.name.replaceAll(' ', '_');
        if (!name.toLowerCase().includes('id')) {
          merm += `  ${attr.type} ${name}\n`;
        }
      }
      merm += '}\n\n';
    }
  
    for (const rel of data.relations) {
      merm += `${rel.source} ${source_relations[rel.cardinality_of_source]}--${target_relations[rel.cardinality_of_target]}${rel.target}: ${rel.name}\n`;
    }
  
    console.log(merm);
    return merm;
  }
    
// Example of using the render function
export async function createMermaidDiagram(data) {
    let element = document.querySelector('#merm-graph');
    let parent = document.querySelector('#nav-mermaid');
    const { svg } = await mermaid.render('merm-graph', convert(JSON.parse(data)));
    element.innerHTML = svg;
    parent.appendChild(element);
    saveFile(new Blob([svg]), 'svg', 'Mermaid')
};