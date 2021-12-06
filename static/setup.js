$(document).ready(function() {
  console.log("I ran!")

  $("#creategamebutton").click(function() {
    let starting_pieces = $("#startingpieces").val();
    let height = $("#height").val();
    let width = $("#width").val();
    let en_passant = $("#enpassant").val();
    let castling = $("#castling").val();

    if (!height) {
      height = 8;
    }
    if (!width) {
      width = 8;
    }
    height = Math.max(1, height);
    height = Math.min(100, height);
    width = Math.max(1, width);
    width = Math.min(100, width);
    if (!starting_pieces) {
      starting_pieces = "STANDARD";
    }

    if (starting_pieces.length > 1000) {
      starting_pieces = starting_pieces.splice(1000, starting_pieces.length - 1000);
    }

    rules_obj = {
      "en_passant": en_passant,
      "castling": castling,
      "starting_pieces": starting_pieces,
      "height": height,
      "width": width
    };
    rules = JSON.stringify(rules_obj);
    console.log(rules);

    $.ajax({
      url: '/start/',
      type: 'POST',
      data: rules,
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      async: false,
      success: function(msg) {
          let game_id = msg.game_id;
          let redirect_loc = "/play/" + game_id;
          console.log(`Redirecting to ${redirect_loc}`);
          window.location.href = redirect_loc;
      }
    });

  });
});
