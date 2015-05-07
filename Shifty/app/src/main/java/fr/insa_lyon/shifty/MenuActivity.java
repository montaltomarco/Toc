package fr.insa_lyon.shifty;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import org.json.JSONArray;
import org.json.JSONObject;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;

public class MenuActivity extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_menu, menu);
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

    public void ButtonOnClickTrajet(View v) {
        Intent nextView;
        switch (v.getId()) {
            case R.id.button_trajet:
                nextView = new Intent(getApplicationContext(),HomeActivity.class);
                startActivity(nextView);
                break;
            case R.id.button_decon:
                nextView = new Intent(getApplicationContext(),MainActivity.class);
                startActivity(nextView);
                break;
        }
    }
}
