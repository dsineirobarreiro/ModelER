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
    //document.getElementById('loader').style.visibility = 'visible';
    var formData = new FormData(form);
    var url = formData.get("url");
    const request = new Request(
        url,
        {
            method: 'POST',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                'X-CSRFToken': csrfToken,
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
        .then(async (response) => {
            if (response.ok) {
                //document.getElementById('loader').style.display = 'none';
                return response.body;
            }
            throw new Error('Network response was not ok.');
        })
        .then(async function(data) {
            let measurementsReceived = 0;
            for await (const measurement of parseJsonStream(data)) {
                measurementsReceived++;
                // To prevent the console from flooding we only show 1 in every 100 measurements
                for (const [key, value] of Object.entries(measurement)) {
                    console.log(`${key}: ${value}`);
                }
            }
        });
}

async function *parseJsonStream(readableStream) {
    for await (const line of readLines(readableStream.getReader())) {
        const trimmedLine = line.trim().replace(/,$/, '');

        if (trimmedLine !== '[' && trimmedLine !== ']') {
            yield JSON.parse(trimmedLine);
        }
    }
}

async function *readLines(reader) {
    const textDecoder = new TextDecoder();
    let partOfLine = '';
    for await (const chunk of readChunks(reader)) {
        const chunkText = textDecoder.decode(chunk);
        const chunkLines = chunkText.split('\n');
        if (chunkLines.length === 1) {
            partOfLine += chunkLines[0];
        } else if (chunkLines.length > 1) {
            yield partOfLine + chunkLines[0];
            for (let i=1; i < chunkLines.length - 1; i++) {
                yield chunkLines[i];
            }
            partOfLine = chunkLines[chunkLines.length - 1];
        }
    }
}

function readChunks(reader) {
    return {
        async* [Symbol.asyncIterator]() {
            let readResult = await reader.read();
            while (!readResult.done) {
                yield readResult.value;
                readResult = await reader.read();
            }
        },
    };
}

//// Events
form.addEventListener('submit', sendForm);

let eventSource;
const sseData = document.getElementById('sse-data');

$(document).ready(function(){
    startSSE();
});

function startSSE() {
    eventSource = new EventSource('http://localhost:8000/modeler/stream/');
    eventSource.onmessage = function (ev) {
        if (ev.data == "$")
            eventSource.close();
        else
            sseData.innerHTML += ev.data;
    };
}