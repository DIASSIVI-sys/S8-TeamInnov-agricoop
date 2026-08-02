    (function () {
      var btnOuvrir = document.getElementById("btn-ouvrir-formulaire");
      var btnAnnuler = document.getElementById("btn-annuler-membre");
      var section = document.getElementById("section-nouveau-membre");
      var form = document.getElementById("form-nouveau-membre");

      function ouvrirFormulaire() {
        section.classList.remove("hidden");
        section.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      function fermerFormulaire() {
        section.classList.add("hidden");
        form.reset();
      }

      btnOuvrir.addEventListener("click", ouvrirFormulaire);
      btnAnnuler.addEventListener("click", fermerFormulaire);

      // Met à jour le sous-titre une fois que main.js a injecté les membres
      // dans #liste-membres (purement cosmétique, ne touche pas à la logique).
      var listeMembres = document.getElementById("liste-membres");
      var sousTitre = document.getElementById("sous-titre-membres");

      function majSousTitre() {
        var nb = listeMembres.querySelectorAll(".membre-ligne").length;
        if (nb > 0) {
          sousTitre.textContent = "Gérez les profils et suivez les soldes de vos " + nb + " producteur" + (nb > 1 ? "s" : "") + " actif" + (nb > 1 ? "s" : "") + ".";
        }
      }

      new MutationObserver(majSousTitre).observe(listeMembres, { childList: true });
      majSousTitre();
    })();
