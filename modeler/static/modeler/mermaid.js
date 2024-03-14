import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.mjs';
mermaid.initialize({ startOnLoad: false });
    
// Example of using the render function
export async function createMermaidDiagram(data) {
    let element = document.querySelector('#merm-graph');
    let parent = document.querySelector('#mermaid');
    const { svg } = await mermaid.render('merm-graph', data);
    element.innerHTML = svg;
    parent.appendChild(element);
};