document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form_js').onsubmit = () => {
        alert("Searching")
        var request = new XMLHttpRequest();
        var myInput = document.querySelector('#myInput').value;
        console.log(myInput)
        request.open("POST", "/api/search");
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.send(JSON.stringify({ "search": myInput}));
        request.onload = () => {

            // Extract JSON data from request
            var data = JSON.parse(request.responseText);
            // Update the result div
            if (data) {
                var contents = "";
                let json_data = data["bookdata"];
                for (x in json_data) {
                    contents += '<a class="item" id="#book_details" href="#" ' + 'onclick=generate_book_details('+json_data[x]["isbn"]+')' + '> <div class="content" style="border: 1px solid black"> <div class="header"><b>'+ json_data[x]["title"]+'   --->   '+ json_data[x]["isbn"] +'</b></div></div></a>'
                }
                document.querySelector('#result').innerHTML = contents;
            }
            else {
                console.log('bye');
                print('bye')
                document.querySelector('#result').innerHTML = 'There was an error.';
            }
        }

        // Add data to send with request
        const data = new FormData();
        data.append('myInput', myInput);
        // request.send(data);
        return false;
    };

});

function generate_book_details(isbn) {
    alert("Fetching Data")
    var request = new XMLHttpRequest();
    console.log('/api/book?isbn='+isbn)
    request.open('GET', '/api/book?isbn='+isbn);
    console.log('hi')
    request.onload = function() {
        console.log("Hello 2.0")
        console.log("Request status"+request.status)
        // console.log("----------"+request.responseText)
        if (request.status === 200) {
            console.log("Hello")
            let data=JSON.parse(request.responseText);
            // let data2 = data["bookdetails"];
            console.log("4.00",data)
            const content = '<div class="content" style="border: 1px solid black"> <div class = "Book">'+
                +'<div class="flex-container"> <section class="container" style="display: flex;"> <div class="left-half">'+
                +'<article><center><img src ='+ data.img +' alt = "Image of a Book"></center></article> </div>'+
                +'<div class="right-half"><article><div class = "details"><br><br><br><center><center><p>Book Name : '+ data.name +'</p>'+
                +'<p>Author : '+data.author+'</p><p>ISBN : '+data.isbn+'</p><p>Year of Publication : '+data.year+'</p><p>Average Rating : </p><p>Number of reviewers : </p></center>'+
                +'</div></article></div></section></div></div>';
            // for (x in data2) {
            //     console.log("hi2.0")
            //     console.log("Hello 3.0", data2[x]["author"])
            //     const content = '<div class="content" style="border: 1px solid black"> <div class = "Book">'+
            //     +'<div class="flex-container"> <section class="container" style="display: flex;"> <div class="left-half">'+
            //     +'<article><center><img src ='+ data2[x]["img"] +' alt = "Image of a Book"></center></article> </div>'+
            //     +'<div class="right-half"><article><div class = "details"><br><br><br><center><center><p>Book Name : '+ data2[x]["name"] +'</p>'+
            //     +'<p>Author : '+data2[x]["author"]+'</p><p>ISBN : '+data2[x]["isbn"]+'</p><p>Year of Publication : '+data2[x]["year"]+'</p><p>Average Rating : '+data2[x]["ratings_count"]+'</p><p>Number of reviewers : '+data2[x]["reviews_count"]+'</p></center>'+
            //     +'</div></article></div></section></div></div>';
            // }
            
            document.querySelector('#book_details').innerHTML = content;
        }
        else {
            document.querySelector('#book_details').innerHTML = "Error";
        }
    };
    request.send();
    // return false;
}