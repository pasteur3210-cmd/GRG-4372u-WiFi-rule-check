import json,threading,tkinter as tk
from tkinter import filedialog,messagebox,ttk
from pathlib import Path
from validator import DEFAULTS,analyze,VERSION

class App(tk.Tk):
 def __init__(self):
  super().__init__();self.title('Shipping Data Validation Tool V'+VERSION);self.geometry('900x690');self.minsize(750,560)
  self.file=tk.StringVar();self.dest=tk.StringVar();self.controls={}
  root=ttk.Frame(self,padding=12);root.pack(fill='both',expand=True)
  ttk.Label(root,text='Shipping Data Validation Tool V'+VERSION,font=('Segoe UI',16,'bold')).pack(anchor='w')
  row=ttk.Frame(root);row.pack(fill='x',pady=6)
  ttk.Label(row,text='Input Excel').pack(side='left');ttk.Entry(row,textvariable=self.file).pack(side='left',fill='x',expand=True,padx=8)
  ttk.Button(row,text='Browse',command=self.browse).pack(side='left')
  row=ttk.Frame(root);row.pack(fill='x',pady=6)
  ttk.Label(row,text='Output folder').pack(side='left');ttk.Entry(row,textvariable=self.dest).pack(side='left',fill='x',expand=True,padx=8)
  ttk.Button(row,text='Browse',command=self.browse_out).pack(side='left')
  ttk.Label(root,text='Rules (editable; saved in report)',font=('Segoe UI',11,'bold')).pack(anchor='w',pady=(12,5))
  frame=ttk.Frame(root);frame.pack(fill='both',expand=True)
  cv=tk.Canvas(frame,highlightthickness=0);scroll=ttk.Scrollbar(frame,orient='vertical',command=cv.yview);inside=ttk.Frame(cv)
  inside.bind('<Configure>',lambda e:cv.configure(scrollregion=cv.bbox('all')))
  cv.create_window((0,0),window=inside,anchor='nw');cv.configure(yscrollcommand=scroll.set);cv.pack(side='left',fill='both',expand=True);scroll.pack(side='right',fill='y')
  for i,(k,v) in enumerate(DEFAULTS.items()):
   ttk.Label(inside,text=k,width=31).grid(row=i,column=0,sticky='w',padx=5,pady=2)
   var=tk.BooleanVar(value=v) if isinstance(v,bool) else tk.StringVar(value=str(v));self.controls[k]=var
   widget=ttk.Checkbutton(inside,variable=var) if isinstance(v,bool) else ttk.Entry(inside,textvariable=var,width=55)
   widget.grid(row=i,column=1,sticky='ew',padx=5,pady=2)
  footer=ttk.Frame(root);footer.pack(fill='x',pady=10)
  self.go=ttk.Button(footer,text='RUN VALIDATION',command=self.run);self.go.pack(side='left')
  self.state=tk.StringVar(value='Ready');ttk.Label(footer,textvariable=self.state).pack(side='left',padx=15)
  self.console=tk.Text(root,height=6,wrap='word');self.console.pack(fill='x')
 def browse(self):
  p=filedialog.askopenfilename(filetypes=[('Excel files','*.xlsx')]);
  if p:self.file.set(p);self.dest.set(str(Path(p).parent/'Shipping_Validation_Result'))
 def browse_out(self):
  p=filedialog.askdirectory();
  if p:self.dest.set(p)
 def run(self):
  if not Path(self.file.get()).is_file():messagebox.showerror('Input','Choose valid xlsx');return
  if not self.dest.get():messagebox.showerror('Output','Choose output folder');return
  cfg={k:v.get() for k,v in self.controls.items()};self.go.state(['disabled']);self.state.set('Running...')
  def worker():
   try:
    result=analyze(self.file.get(),self.dest.get(),cfg)
    self.after(0,lambda:self.done(result))
   except Exception as ex:
    self.after(0,lambda msg=str(ex):self.error(msg))
  threading.Thread(target=worker,daemon=True).start()
 def done(self,result):
  self.go.state(['!disabled']);self.state.set(f"PASS {result['pass']} / FAIL {result['fail']}")
  self.console.insert('end',json.dumps(result,ensure_ascii=False,indent=2)+'\n');self.console.see('end');messagebox.showinfo('Finished',f"Report: {result['report']}\nPASS: {result['pass']} FAIL: {result['fail']}")
 def error(self,msg):self.go.state(['!disabled']);self.state.set('ERROR');self.console.insert('end',msg+'\n');messagebox.showerror('Validation error',msg)
if __name__=='__main__':App().mainloop()
