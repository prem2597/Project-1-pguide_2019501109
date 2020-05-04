document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form_js').onsubmit = () => {
        alert("Searching please wait!")
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
                    console.log('check',json_data[x]["isbn"]);
                    console.log(typeof(json_data[x]["isbn"]));
                    contents += '<a class="item" id="#book_details" href="#" ' + 'onclick=generate_book_details("'+json_data[x]["isbn"]+'")' + '> <div class="content" style="border: 1px solid black"> <div class="header"><b>'+ json_data[x]["title"]+'</b></div></div></a>'
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
    alert("Fetching Data   please wait!")
    console.log(typeof(isbn))
    var request = new XMLHttpRequest();
    console.log('/api/book?isbn='+isbn)
    // print('------------------'+isbn)
    request.open('GET', '/api/book?isbn='+isbn);
    console.log('hi')
    request.onload = function() {
        console.log("Hello 2.0")
        console.log("Request status"+request.status)
        console.log("----------"+request.responseText)
        if (request.status === 200) {
            console.log("Hello")
            let data=JSON.parse(request.responseText);
            // let data2 = data["bookdetails"];
            console.log(request.responseText)
            console.log("4.00",data)
            // console.log(data[0]["img"])
            // const content = '<div class="content" style="border: 1px solid black"> <div class = "Book">'+
            //     +'<div class="flex-container"> <section class="container" style="display: flex;"> <div class="left-half">'+
            //     +'<article><center><img src ='+ data[0]["img"] +' alt = "Image of a Book"></center></article> </div>'+
            //     +'<div class="right-half"><article><div class = "details"><br><br><br><center><center><p>Book Name : '+ data[0]["name"] +'</p>'+
            //     +'<p>Author : '+data[0]["author"]+'</p><p>ISBN : '+data[0]["isbn"]+'</p><p>Year of Publication : '+data[0]["year"]+'</p><p>Average Rating : '+data[0]["ratings_count"]+'</p><p>Number of reviewers : '+data[0]["reviews_count"]+'</p></center>'+
            //     +'</div></article></div></section></div></div>';
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
            const content = '<div class="content" style="border: 1px solid black">'+
            '<div class = "name"><h1>Display Board</h1></div><hr class="new4">'+
            '<div class = "Book"><div class="flex-container"><section class="container" style="display: flex;">'+
            '<div class="left-half"><article><center><img src ="'+data[0]["img"]+'" alt = "Image of a Book"></center></article></div>'+
            '<div class="right-half"><article><div class = "details"><br><br><br>'+
            '<center><p>Book Name : "'+data[0]["title"]+'"</p><p>Author : "'+data[0]["author"]+'"</p><p>ISBN : "'+data[0]["isbn"]+'"</p><p>Year of Publication : "'+data[0]["year"]+'"</p><p>Average Rating : "'+data[0]["rating"]+'"</p><p>Number of reviewers : "'+data[0]["review"]+'"</p></center>'+
            '</div></article></div></section></div><hr class="new3"><center><div class = "button"><h3>Your Review</h3><br>'+
            '<form method="POST" class="form-border"><div class="flex-container"><section class="container" style="display: flex;">'+
            '<div class="left-half"><article><br><br><br><br><br><div class = "select3"><label for="rating" style = "font-weight: bold; color: black;">Rate this book</label>'+
            '<select id="rating" name="rating" class="form-control" required><option value="1">1</option><option value="2">2</option>'+
            '<option selected value="3">3</option><option value="4">4</option><option value="5">5</option></select></div></article></div>'+
            '<div class="right-half"><article><div class="rating-input"><br>'+
            '<textarea name="matter" style= "color: black;" id="review" class="form-control" rows="10" placeholder="Write your review here" required></textarea>'+
            '</div></article></div></section></div><div><button class="rating-btn" type="submit">{{Submit}}</button></div></form></div></center></div>'+
            '<hr class="new3">{% has to be implemented for review %}<div class = "review" style = "display: flex; justify-content: center; color: black; float: top; font-style: normal; font-weight: bolder; font-size: x-small;">'+
            '<ul><center><li style = "font-size: 20px; font-style: normal;">Your Previous Rating & Review</li><hr class="new3">'+
            '<li style = "font-size: 20px; font-style: normal;">{{rating_data}}/5</li><br><li style = "color: black; font-size: 20px;">{{Review}}</li></center>'+
            '</ul></div>{% has to be implemented for review %}</div></div>'

            
            document.querySelector('#book_details').innerHTML = content;
        }
        else {
            document.querySelector('#book_details').innerHTML = "Error";
        }
    };
    request.send();
    // return false;
}