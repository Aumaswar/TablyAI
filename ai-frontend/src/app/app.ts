import { Component, ChangeDetectorRef } from '@angular/core';

import { CommonModule } from '@angular/common';

import { FormsModule } from '@angular/forms';
import * as XLSX from 'xlsx';
import {
  HttpClient,
  HttpClientModule,
  HttpHeaders
} from '@angular/common/http';

@Component({

  selector: 'app-root',

  standalone: true,

  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule
  ],

  templateUrl: './app.html',

  styleUrls: ['./app.css']

})

export class AppComponent {
  
  
  host = '';

  username = '';

  password = '';

  database = '';

  dbType = 'mysql';

  question = '';

  responseData: any = null;

  schemaData: any = null;

  loading = false;

  token = '';

  appUsername = '';

  appPassword = '';

  metadataTable = '';

  metadataColumn = '';

  metadataDescription = '';
  
  tables: string[] = [];

  columns: string[] = [];
  loadTables() {

  this.http.get<any>(
    'http://localhost:8000/tables'
  ).subscribe({

    next: (response) => {

      this.tables = response;

    },

    error: (error) => {

      console.error(error);

    }

  });

}
loadColumns() {

  this.columns = [];

  this.metadataColumn = '';

  if (!this.metadataTable) {

    return;

  }

  this.http.get<any>(
    `http://localhost:8000/columns/${this.metadataTable}`
  ).subscribe({

    next: (response) => {

      this.columns = response;

    },

    error: (error) => {

      console.error(error);

    }

  });

}
  constructor(

  private http: HttpClient,

  private cdr: ChangeDetectorRef

) {

  this.host =
    localStorage.getItem(
      'db_host'
    ) || '';

  this.username =
    localStorage.getItem(
      'db_username'
    ) || '';

  this.database =
    localStorage.getItem(
      'db_database'
    ) || '';

  this.dbType =
    localStorage.getItem(
      'db_type'
    ) || 'mysql';

}

  login() {

    const body = {

      username: this.appUsername,

      password: this.appPassword

    };

    this.http.post(

      'http://localhost:8000/login',

      body

    ).subscribe({

      next: (response: any) => {

        console.log(response);
        console.log(
  "LOGIN RESPONSE:",
  response
);

console.log(
  "ACCESS TOKEN:",
  response.access_token
);
        this.token = response.access_token;

        localStorage.setItem(
          'token',
          this.token
        );
        console.log(
    "STORED:",
    localStorage.getItem("token")
  );
        alert('Login successful');

      },

      error: (error) => {

        console.error(error);

        alert('Login failed');

      }

    });

  }

  logout() {

    this.token = '';

    localStorage.removeItem('token');

    alert('Logged out');

  }

connectDB() {

  const body = {

    db_type: this.dbType,

    host: this.host,

    username: this.username,

    password: this.password,

    database: this.database

  };

  this.http.post(

    'http://localhost:8000/connect-db',

    body

  ).subscribe({

    next: (response: any) => {

  console.log(response);

  localStorage.setItem(
    'db_host',
    this.host
  );

  localStorage.setItem(
    'db_username',
    this.username
  );

  localStorage.setItem(
    'db_database',
    this.database
  );

  localStorage.setItem(
    'db_type',
    this.dbType
  );

  alert(response.message);

  this.loadTables();

},

    error: (error) => {

      console.error(error);

      alert('Connection failed');

    }

  });

}

  saveMetadata() {

    const token = localStorage.getItem(
      'token'
    );

    const headers = new HttpHeaders({

      Authorization: `Bearer ${token}`

    });

    const body = {

      table_name: this.metadataTable,

      column_name: this.metadataColumn,

      description: this.metadataDescription

    };

    this.http.post(

      'http://localhost:8000/save-metadata',

      body,

      { headers }

    ).subscribe({

      next: (response: any) => {

        console.log(response);

        alert('Metadata saved');

        this.metadataTable = '';

        this.metadataColumn = '';

        this.metadataDescription = '';

      },

      error: (error) => {

  console.log(error);

  if (error.error) {

    alert(
      JSON.stringify(error.error)
    );

  } else {

    alert('Failed to save metadata');

  }

}
    });

  }

  askAI() {

    if (!this.question.trim()) {

      alert('Please enter a question');

      return;

    }

    const token = localStorage.getItem(
      'token'
    );

    const headers = new HttpHeaders({

      Authorization: `Bearer ${token}`

    });

    this.loading = true;

    this.responseData = null;

    this.http.get(

      `http://localhost:8000/query?question=${encodeURIComponent(this.question)}`,

      { headers }

    ).subscribe({

      next: (response: any) => {

        console.log(response);

        this.responseData = response;

        this.loading = false;

        this.cdr.detectChanges();

      },

      error: (error) => {

        console.error(error);

        this.loading = false;

        alert('Query failed');

      }

    });

  }

  loadSchema() {

    this.http.get(

      'http://localhost:8000/schemas'

    ).subscribe({

      next: (response: any) => {

        console.log(response);

        this.schemaData = response;

        this.cdr.detectChanges();

      },

      error: (error) => {

        console.error(error);

        alert('Failed to load schema');

      }

    });

  }

  objectKeys(obj: any): string[] {

    return Object.keys(obj);

  }
  exportToExcel() {

  if (!this.responseData?.result?.length) {

    alert('No data to export');
    return;

  }

  const worksheet = XLSX.utils.json_to_sheet(
    this.responseData.result
  );

  const workbook = XLSX.utils.book_new();

  XLSX.utils.book_append_sheet(
    workbook,
    worksheet,
    'Results'
  );

  XLSX.writeFile(
    workbook,
    'AI_Query_Result.xlsx'
  );

}
}