package fr.insa_lyon.shifty;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;

/**
 * Created by marcomontalto on 06/05/15.
 */
public class AddressChoiceActivity extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_choice_address);
        Bundle b = getIntent().getExtras();
        if(b!=null)
        {
            int value = b.getInt("result");
            System.out.println("Result is : " +  value);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_choice_address, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void ButtonOnClickValidate(View v) {
        Intent nextView;
        switch (v.getId()) {
            case R.id.button_NouvelleRecherche:
                System.out.println("************  button nouvelle Recherche   ******************");
                //on passe à la vue suivante
                nextView = new Intent(getApplicationContext(),HomeActivity.class); //A changer par une vue avec la liste des addresses proposees
                startActivity(nextView);
                break;
            case R.id.button_Valider: //Pourquoi il aurait il un bouton inscription dans homeActivity?
                System.out.println("************  button valider   ******************");
                nextView = new Intent(getApplicationContext(),AddressChoiceActivity.class); //A changer par une vue avec la liste des addresses proposees
                startActivity(nextView);
                break;
        }
    }
}
