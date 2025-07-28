(function (define) {
    "use strict";

    define(["jquery"], function ($) {
        return function HutechNewsWidget() {
            var $widget = $(".hutech-news-widget");

            // Thêm hiệu ứng khi hover vào tin tức
            $widget.find(".hutech-news-item").hover(
                function () {
                    $(this).css("background-color", "#f9f9f9");
                },
                function () {
                    $(this).css("background-color", "transparent");
                }
            );

            // Nếu muốn cập nhật tin tức từ API mà không reload trang
            function refreshNews() {
                $.ajax({
                    url: "/hutech-news/api/news/",
                    type: "GET",
                    success: function (data) {
                        var $newsItems = $widget.find(".hutech-news-items");
                        $newsItems.empty();

                        if (data.news && data.news.length > 0) {
                            $.each(data.news, function (index, item) {
                                var newsHtml = '<div class="hutech-news-item">';

                                if (item.image_url) {
                                    newsHtml +=
                                        '<div class="hutech-news-image">' + '<img src="' + item.image_url + '" alt="' + item.title + '">' + "</div>";
                                }

                                newsHtml +=
                                    '<div class="hutech-news-content">' +
                                    '<h4><a href="' +
                                    item.url +
                                    '" target="_blank">' +
                                    item.title +
                                    "</a></h4>" +
                                    '<p class="hutech-news-date">' +
                                    formatDate(new Date(item.published_date)) +
                                    "</p>";

                                if (item.summary) {
                                    newsHtml +=
                                        '<p class="hutech-news-summary">' +
                                        (item.summary.length > 100 ? item.summary.substring(0, 97) + "..." : item.summary) +
                                        "</p>";
                                }

                                newsHtml += "</div></div>";

                                $newsItems.append(newsHtml);
                            });
                        } else {
                            $newsItems.html("<p>Không có tin tức mới từ HUTECH.</p>");
                        }
                    },
                    error: function () {
                        console.error("Failed to fetch HUTECH news");
                    },
                });
            }

            function formatDate(date) {
                return ("0" + date.getDate()).slice(-2) + "/" + ("0" + (date.getMonth() + 1)).slice(-2) + "/" + date.getFullYear();
            }

            // Cập nhật tin tức mỗi 30 phút
            // setInterval(refreshNews, 30 * 60 * 1000);

            return {
                // Phương thức có thể gọi từ bên ngoài
                refresh: refreshNews,
            };
        };
    });
}).call(this, define || RequireJS.define);
