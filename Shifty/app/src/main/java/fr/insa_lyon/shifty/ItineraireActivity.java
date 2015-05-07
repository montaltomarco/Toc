package fr.insa_lyon.shifty;

import android.app.ListActivity;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.RadioButton;
import android.widget.RadioGroup;

import org.json.JSONObject;

import java.util.ArrayList;


public class ItineraireActivity extends ListActivity {

    private String[] mStrings;
    private JSONObject response;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_itineraire);

        Bundle b = getIntent().getExtras();

        if(b!=null)
        {
            String value = b.getString("result");
            ArrayList<String> listeRes = new ArrayList<String>();
            listeRes.add(value);
            listeRes.add("AAAAAAAAAAAAAAAAAAAAAAAAAAa");
            listeRes.add("BBBBBBBBBBBBBBBBBBBBBBBBBB");
            mStrings=listeRes.toArray(new String[listeRes.size()]);

            /*try {
                response = new JSONObject(value);

                for (int i = 0; i < response.getJSONArray("indications").length(); i++) {
                    mStrings[i] = response.getJSONArray("indications").getJSONObject(i).getString("name");
                }

            } catch (Exception e) {
                e.printStackTrace();
            }*/
        }


        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1, mStrings);
        setListAdapter(adapter);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_itineraire, menu);
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
}
