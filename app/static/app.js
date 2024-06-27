$(document).ready(function () {
  const scoreUrl = $(".content").data("score-url");
  const topUsersUrl = $(".content").data("top-users-url");

  $("#counterBtn").click(function () {
    $.ajax({
      type: "POST",
      url: scoreUrl,
      success: function (response) {
        $("#count").text(response.score);
      },
    });
  });

  updateLeaderboard();

  setInterval(updateLeaderboard, 500);

  function updateLeaderboard() {
    $.ajax({
      type: "GET",
      url: topUsersUrl,
      dataType: "json",
      success: function (response) {
        var leaderboardBody = $("#leaderboard-body");
        leaderboardBody.empty();
        $.each(response.top_users, function (index, user) {
          var row = $("<tr>");
          row.append($("<td>").text(index + 1));
          row.append($("<td>").text(user.username));
          row.append($("<td>").text(user.score));
          leaderboardBody.append(row);
        });
      },
      error: function (xhr, status, error) {
        console.error("Error updating leaderboard:", error);
      },
    });
  }
});
