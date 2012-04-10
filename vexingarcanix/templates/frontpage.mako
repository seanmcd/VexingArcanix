<%inherit file="shell.mako" />

<%block name="main_content">
    ${self.deck_upload()}
</%block>

<%def name="deck_upload()">
    <div id="deck_form" style="margin: auto; text-align: center;">
        <hr>
        <h2>Please enter a deck</h2>
	<div class="tab" id="mtg_tab">
          <form action="/check" method="post">
            <textarea rows="25" cols="40" name="deck_list_area" id="deck_list">
	      15 Lightning Bolt
	      15 Grizzly Bears
	      5 Fireball
	      5x Gruul Signet'
	      5 Mountains
	      5xForest
	      5   Fire-Lit Thicket
	      5 "Rootbound Crag"
	    </textarea>
            <br>
            <input type="submit" value="Upload this decklist">
          </form>
	</div>
	<div class="tab" id="pokemon_tab">
          <form action="/check" method="post">
            <textarea rows="25" cols="40" name="deck_list_area" id="deck_list">
	      4       Celebi (TR 92)
	      4       Mewtwo EX (ND 98)

	      4       N (NV 101)
	      4       Professor Oak's New Theory (HGSS 101)
	      4       Professor Juniper (BW 101)
	      4       Junk Arm (TR 87)
	      4       Dual Ball (UL 72)
	      4       Pokemon Catcher (EP 95)
	      4       Switch (HGSS 102)
	      2       Eviolite (NV 91)
	      2       Skyarrow Bridge (ND 91)
	      3       PlusPower (UL 80)
	      1       Energy Retrieval (BW 92)
	      2       Pokegear 3.0 (HGSS 96)
	      1       Seeker (TR 88)

	      9       Grass Energy (HGSS 115)
	      4       Double Colorless Energy (ND 92)
            </textarea>
            <br>
            <input type="submit" value="Upload this decklist">
          </form>
        </div>
    </div>
</%def>
