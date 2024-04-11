import { createJointDiagram } from './joint.js'
import { createMermaidDiagram } from './mermaid.js'
import { createUmlDiagram } from './plantUml.js';

let input = document.querySelector("#id_prompt");
let button = document.querySelector(".send-btn");

button.disabled = true; //setting button state to disabled


input.addEventListener("input", updateValue);

function updateValue(e) {
    input.value = e.target.value;
    if (input.value === "") {
        button.disabled = true; //button remains disabled
    } else {
        button.disabled = false; //button is enabled
    }
}


//// Variables
// Get csrf token
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const form = document.querySelector('#promptForm');

//// Functions

function sendForm(event) {
    event.preventDefault();
    var url = 'http://127.0.0.1:8001/generate'
    document.getElementById('loader').style.visibility = 'visible';
    var formData = new FormData(form);
    const request = new Request(
        url,
        {
            method: 'POST',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                'X-CSRFToken': csrfToken,
                'ngrok-skip-browser-warning': 'true'
            },
            body: formData,
        }
    );
    document.getElementById('promptForm').reset();
    //setting inputs state to disabled
    button.disabled = true; 
    input.disabled = true;
    var chat = document.getElementById('chat');
    chat.innerHTML += `
    <div class="message">
        <div class="response">
            <p class="text">${formData.get('prompt')}</p>
        </div>
    </div>
    `;
    
    fetch(request)
        .then((response) => {
            if (response.ok) {
                document.getElementById('loader').style.display = 'none';
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(async function(data) {
            console.log(data);

            createJointDiagram(data['raw']);
            createMermaidDiagram(data['mermaid']);
            createUmlDiagram(data['uml']);

            input.disabled = false;
        });
}

//// Events
form.addEventListener('submit', sendForm);