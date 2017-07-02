$('.residents').click(function(event){
    var planetName = event.target.dataset.name;
    var links = event.target.dataset.links;
    links = links.replace(/\[|\]|\'/g, '');
    if (links.indexOf(',') > -1) {
        links = links.split(', ');
    } else {
        links = [links];
    }
    $('.modal-title').text('Residents of ' + planetName);
    var tableContent = [];
    for (let i = 0; i < links.length; i++){
        $.ajax({
            url: links[i].slice(0, 4) + 's' + links[i].slice(4),
            method: 'GET',
            async: false,
            success: function (data) {
                var personData = [
                data.name,
                data.height !== 'unknown' ? data.height + ' cm': 'unknown',
                data.mass !== 'unknown' ? data.mass + ' kg': 'unknown',
                data.hair_color,
                data.skin_color,
                data.eye_color,
                data.birth_year,
                data.gender
            ];
            tableContent.push(personData);
            }
        });
    }
    var htmlstring = `<table class='table-bordered'>
                <tr>
                    <th>Name</th>
                    <th>Height</th>
                    <th>Mass</th>
                    <th>Hair Clolr</th>
                    <th>Skin color</th>
                    <th>Eye color</th>
                    <th>Birth year</th>
                    <th>Gender</th>
                </tr>`;
    for (let row=0; row < tableContent.length; row++) {
        htmlstring += '<tr>';
        for (let col=0; col < tableContent[row].length; col++) {
            htmlstring += '<td>' + tableContent[row][col] + '</td>';
        }
        htmlstring += '</tr>';
    }
    htmlstring += "</table>"
    debugger;
    $('.modal-body').html(htmlstring);
    $('#myModal').modal('show');
});
