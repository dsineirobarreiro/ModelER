import { bundle } from './bundle.js'
import { saveFile } from './model.js'

const svg = 'https://www.plantuml.com/plantuml/svg/';
const png = 'https://www.plantuml.com/plantuml/png/';

// Get csrf token
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const sourceRelations = {
  "Zero or One": "|o",
  "Exactly One": "||",
  "Zero or Many": "}o",
  "One or Many": "}|"
};
const targetRelations = {
  "Zero or One": "o|",
  "Exactly One": "||",
  "Zero or Many": "o{",
  "One or Many": "|{"
};

function convert(data) {
    let uml = '@startuml\n';
    for (let entity of data.entities) {
        uml += 'entity ' + entity.name + '{\n';
        uml += '* ' + entity.name + 'ID: number <<generated>>\n--\n';
        for (let attribute of entity.attributes) {
            if (attribute.name.toLowerCase().includes('id')) continue;
                uml += '* ' + attribute.name + ': ' + attribute.type + '\n';
            }
        uml += '}\n\n';
    }

    for (let relation of data.relations) {
        uml += relation.source + ' ' + sourceRelations[relation.cardinality_of_source] + '--' + targetRelations[relation.cardinality_of_target] + relation.target + '\n';
    }

    uml += '@enduml';
    return uml
}

export function createUmlDiagram(data){
    let encode = bundle(convert(JSON.parse(data)));
    const pngRequest = new Request(
        png + encode,
        {
            method: 'GET',
        }
    );
    fetch(pngRequest)
        .then((response) => {
            if (response.ok) {
                return response.blob()
            }
            throw new Error('Network response was not ok.');
        })
        .then(function(data) {
            saveFile(data, 'png', 'Plantuml')
            let img = document.querySelector('#plant-diagram')
            img.setAttribute('src', png+encode);
        });
}