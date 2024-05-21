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

$("#promptForm").on("submit", function(event) {
    event.preventDefault();
    var formData = new FormData(form);
    console.log(formData.get('prompt'));
    var url = 'http://localhost:8001/llama/generate/';
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
    
    fetch(request)
        .then(async (response) => {
            if (response.ok) {
                //document.getElementById('loader').style.display = 'none';
                chat.innerHTML += `
                    <div class="message">
                        <div class="response">
                            <p class="text">${formData.get('prompt')}</p>
                        </div>
                    </div>
                `;
                return response.body;
            }
            throw new Error('Network response was not ok.');
        })
        .then(async function(data) {
            console.log(data)
        })
})

function sendForm(event) {
    event.preventDefault();
    //document.getElementById('loader').style.visibility = 'visible';
    var formData = new FormData(form);
    console.log(formData.get('prompt'));
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
    
    fetch(request)
        .then(async (response) => {
            if (response.ok) {
                //document.getElementById('loader').style.display = 'none';
                chat.innerHTML += `
                    <div class="message">
                        <div class="response">
                            <p class="text">${formData.get('prompt')}</p>
                        </div>
                    </div>
                `;
                return response.body;
            }
            throw new Error('Network response was not ok.');
        })
        .then(async function(rb) {
            /*let measurementsReceived = 0;
            for await (const measurement of parseJsonStream(data)) {
                measurementsReceived++;
                // To prevent the console from flooding we only show 1 in every 100 measurements
                for (const [key, value] of Object.entries(measurement)) {
                    console.log(`${key}: ${value}`);
                }
            }*/
            const reader = rb.getReader();

            let msgId = 1;

            chat.innerHTML += `
                <div class="message">
                    <p class="text" id=r-${msgId}></p>
                </div>
            `;
            var msg = document.getElementById('r-1');

            return new ReadableStream({
                start(controller) {
                    // The following function handles each data chunk
                    function push() {
                        // "done" is a Boolean and value a "Uint8Array"
                        reader.read().then(({ done, value }) => {
                            // If there is no more data to read
                            if (done) {
                                console.log("done", done);
                                controller.close();
                                return;
                            }
                            let token = new TextDecoder().decode(value);
                            // Get the data and send it to the browser via the controller
                            controller.enqueue(token);
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
//form.addEventListener('submit', sendForm);

let eventSource;
const sseData = document.getElementById('sse-data');

/*$(document).ready(function(){
    var input = $("<input>")
                    .attr("type", "hidden")
                    .attr("name", "greet").val("Hi, how are you?\n");
    $("#promtpForm").append($(input));
    $("#promptForm").trigger("submit");
});*/

function startSSE() {
    eventSource = new EventSource('http://localhost:8000/modeler/stream/');
    eventSource.onmessage = function (ev) {
        if (ev.data == "$")
            eventSource.close();
        else
            sseData.innerHTML += ev.data;
    };
}