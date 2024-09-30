import { createMermaidDiagram } from './mermaid.js'
import { createUmlDiagram } from './plantUml.js';
import { init } from './gojs.js';

let tooltipTriggerList, tooltipList;

document.addEventListener("DOMContentLoaded", function() {
    tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

    let gojs = document.querySelector('#myDiagramDiv');
    let elements = gojs.getAttribute('data-elements');

    init(elements);
});

let input = document.querySelector("#id_prompt");
let chat = document.querySelector('#chat');
export const dgram = document.querySelector('#diagram');

let msgId = parseInt(chat.getAttribute('data-last-index')) + 1;

let diagram = [];

input.addEventListener("input", updateValue);

function updateValue(e) {
    input.value = e.target.value;
    if (input.value === "") {
        send.disabled = true; //button remains disabled
    } else {
        send.disabled = false; //button is enabled
    }
}


//// Variables
// Get csrf token
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const form = document.querySelector('#promptForm');
const send = document.querySelector('#send');
const gen = document.querySelector('#gen');

send.disabled = true; //setting button state to disabled

//// Functions

function submitForm(event, action) {
    event.preventDefault();
    var formData = new FormData(form);
    formData.append('action', action);
    console.log(formData.get('prompt'));
    var url = window.location.href;
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
    send.disabled = true; 
    input.disabled = true;

    chat.innerHTML += `
                    <div class="message">
                        <div class="response">
                            <p class="text" id="r-${msgId}">${formData.get('prompt')}</p>
                        </div>
                    </div>
                `;
    
    fetch(request)
        .then(async (response) => {
            if (response.ok) {
                return response.body;
            }else{
                var msg = document.getElementById('r-' + msgId);
                msg.className += ' error'
            }
        })
        .then(async function(rb) {
            const reader = rb.getReader();

            msgId++;

            chat.innerHTML += `
                <div class="message">
                    <p class="text" id=r-${msgId}></p>
                </div>
            `;
            var msg = document.getElementById('r-' + msgId);

            msgId++;

            let menu = document.querySelector('#download-menu');
            menu.innerHTML = '';

            return new ReadableStream({
                start(controller) {
                    // The following function handles each data chunk
                    function push() {
                        // "done" is a Boolean and value a "Uint8Array"
                        reader.read().then(({ done, value }) => {
                            // If there is no more data to read
                            if (done) {
                                console.log("done", done);

                                createMermaidDiagram(msg.innerText);
                                createUmlDiagram(msg.innerText);
                                init(msg.innerText);
                                send.disabled = false; 
                                input.disabled = false;
                                controller.close();
                                return;
                            }
                            let token = new TextDecoder().decode(value);
                            // Get the data and send it to the browser via the controller
                            controller.enqueue(token);
                            diagram.push(token);
                            // Check chunks by logging to the console
                            //console.log(done, token);
                            msg.innerText += token;
                            push();
                        });
                    }

                    push();
                },
            });

        })
}

send.addEventListener("click", function(event) {
    submitForm(event, 'generate')
})

/*gen.addEventListener("click", function(event) {
    submitForm(event, 'generate')
})*/

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

export function saveFile(data, format, type){
    const id = dgram.getAttribute('data-diagram-id');
    const url = window.location.origin + '/modeler/diagram/' + id + '/' + format
    let formData = new FormData();
    formData.append('file', data, type + '_' + id + '.' + format);
    formData.append('tool', type[0])
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
    fetch(request)
        .then((response) => {
            if (response.ok) {
                return response.json()
            }
            else throw new Error('Network response was not ok.');
        })
        .then((data) => {
            let item = document.querySelector('#' + data.tool.toLowerCase() + '-' + data.format)
            if (item == null){
                let menu = document.querySelector('#download-menu');
                let html = `
                    <li>
                        <a class="dropdown-item" id="${data.tool.toLowerCase()}-${data.format}" href="${data.path}" download>
                            Download ${data.tool} as ${data.format}
                        </a>
                    </li>
                `;

                menu.innerHTML += html;
            }
            else{
                item.setAttribute('href', data.path)
            }
        })
}
