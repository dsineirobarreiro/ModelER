export function createPlantDiagram(data) {
    typeRelations = {"Zero or One": "|o", "Exactly One": "||", "Zero or Many": "}o", "One or Many": "}|"};
    let mermaid = "@startuml\n";
    let res = JSON.parse(data);
    res["entities"].forEach(drawEntities);
    res["relations"].forEach(drawRelations);
    mermaid += "@enduml"
    return mermaid;
}



function drawEntities(value, index, array) {
    plantUml += "entity " + value.name + " {\n";
    plantUml += "\t* " + value.name + "ID: number <<generated>>\n\t--\n";
    for(x in value.attributes){
        if(value.attributes[x].contains("id")) continue;
        plantUml += "\t* " + value.attributes[x]["name"] + ": " + value.attributes[x]["type"] + "\n"
    }
    plantUml += "}\n\n"
}

function drawRelations(value, index, array) {
    mermaid += value.source + " " + typeRelations[value.cardinality_of_source] + "--" + typeRelations[value.cardinality_of_target] + " " + value.target + "\n"
}