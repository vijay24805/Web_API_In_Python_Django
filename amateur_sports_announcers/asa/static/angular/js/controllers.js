'use strict';

/* Controllers */
var twitterApp = angular.module('twitterApp', [])

twitterApp.controller('TweetListCtrl', function($scope) {
    
    /* my own stuff testing angular */
    var apiKey = 'AIzaSyBvhjAvsELTtd0u9JNi3ZFRGnWx-nzXt8Y';
    function getVideos(keyword) {
        $.ajax({
            type: "GET",
            url: "https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + encodeURIComponent(keyword) + "&type=video&videoEmbeddable=true&key=" + apiKey
        })
        .done(function(data){
            var videos = "";
            for(var i=0; i< data.items.length; i++) {
                videos += '<li><a class="setVideo" id="' + data.items[i].id.videoId + '">' + data.items[i].snip
                pet.title + '</a></li>';
            }
            $("#videos").append(videos);
            $(".setVideo").click(function() {
                $("#youtubeembed").attr('src', '//www.youtube.com/embed/' + $(this).attr('id') + "?autoplay=1");
            });
        });
    } // end function getVideos(keyword)

    
    $scope.tweets = [];
});
