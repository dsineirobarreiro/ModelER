let url = 'https://www.plantuml.com/plantuml/svg/'

export function createUmlDiagram(encode){
    console.log(encode)
    const request = new Request(
        url + encode,
        {
            method: 'GET',
        }
    );
    fetch(request)
        .then((response) => {
            if (response.ok) {
                return response.text()
            }
            throw new Error('Network response was not ok.');
        })
        .then(function(data) {
            $('#plantuml').html(data)
        });

}