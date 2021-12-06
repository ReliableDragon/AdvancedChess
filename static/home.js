$(document).ready(function() {
  console.log("I ran!")

  $("#startnewgame").click(function() {
    let game_id = $("#joingameid").val();
    let redirect_loc = "/start/" + game_id;
    console.log(`Redirecting to ${redirect_loc}`);
    window.location.href = redirect_loc;
  });

  $("#submitjoingame").click(function() {
    let game_id = $("#joingameid").val();
    let redirect_loc = "/join/" + game_id;
    console.log(`Redirecting to ${redirect_loc}`);
    window.location.href = redirect_loc;
  });
});
