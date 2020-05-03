export function generate_book_details(isbn) {
    alert("Fetching Data")
    var request = new XMLHttpRequest();
    request.open('POST', '/api/book?isbn='+isbn);
    request.onload = function() {
        if (request.status === 200) {
            let data=JSON.parse(request.responseText);
            const content = '<div class="content" style="border: 1px solid black"> <div class = "Book">'+
            +'<div class="flex-container"> <section class="container" style="display: flex;"> <div class="left-half">'+
            +'<article><center><img src ='+ data.img +' alt = "Image of a Book"></center></article> </div>'+
            +'<div class="right-half"><article><div class = "details"><br><br><br><center><center><p>Book Name : '+ data.name +'</p>'+
            +'<p>Author : '+data.author+'</p><p>ISBN : '+data.isbn+'</p><p>Year of Publication : '+data.year+'</p><p>Average Rating : '+data.ratings_count+'</p><p>Number of reviewers : '+data.reviews_count+'</p></center>'+
            +'</div></article></div></section></div></div>';
            
            document.querySelector('#book_details').innerHTML = content;
        }
        else {
            document.querySelector('#book_details').innerHTML = "Error";
        }
    };
    request.send();
    return false;
}