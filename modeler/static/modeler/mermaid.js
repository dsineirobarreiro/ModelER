export function createMermaidDiagram(data) {
    typeRelations = {"Zero or One": "|o", "Exactly One": "||", "Zero or Many": "}o", "One or Many": "}|"};
    let mermaid = 'erDiagram\n';
    let res = JSON.parse(data);
    res["entities"].forEach(drawEntities);
    res["relations"].forEach(drawRelations);
    return mermaid;
}



function drawEntities(value, index, array) {
    mermaid += value.name + " {\n";
    mermaid += "int " + value.name + "ID PK\n";
    for(x in value.attributes){
        if(value.attributes[x] == "id") continue;
        mermaid += value.attributes[x]["type"] + " " + value.attributes[x]["name"] + "\n"
    }
    mermaid += "}\n\n"
}

function drawRelations(value, index, array) {
    mermaid += value.source + " " + typeRelations[value.cardinality_of_source] + "--" + typeRelations[value.cardinality_of_target] + " " + value.target + " : " + value.name + "\n"
}