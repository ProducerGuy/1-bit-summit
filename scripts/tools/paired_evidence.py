"""Audit paired retention and split finite-suite seed vs task uncertainty.
Input CSV columns: seed, benchmark, cluster, n, reference_sum, student_sum.
Each row is a cluster aggregate; every seed has the identical cluster set.
No automatic trophy award. Fixed-suite t CI assumes iid normal seed means;
cluster SE is approximate for independent clusters with fixed trained seeds.
For a population of both seeds/tasks, use validated crossed-effects inference.
"""
import argparse,csv,json,math
import numpy as np
from scipy.stats import t, norm, nct

def audit(rows,ratio=0.99,margin=0.):
    seeds=sorted({str(r['seed']) for r in rows});bs=sorted({str(r['benchmark']) for r in rows});S=len(seeds);H=len(bs)
    means=np.zeros(S);taskvar=0.;nobs=0;counts={};refs=np.zeros(S);studs=np.zeros(S)
    for b in bs:
        rr=[r for r in rows if str(r['benchmark'])==b];clusters=sorted({str(r['cluster']) for r in rr});n=len(clusters);C={str(r['cluster']):j for j,r in enumerate([{'cluster':c} for c in clusters])};A={s:i for i,s in enumerate(seeds)}
        x=np.full((S,n),np.nan);ref=x.copy();stu=x.copy();nn=x.copy()
        for r in rr:
            i,j=A[str(r['seed'])],C[str(r['cluster'])];assert np.isnan(x[i,j]),'duplicate';nn[i,j]=float(r['n']);ref[i,j]=float(r['reference_sum']);stu[i,j]=float(r['student_sum']);x[i,j]=stu[i,j]-ratio*ref[i,j]+margin*nn[i,j]
        assert np.isfinite(x).all() and np.isfinite(nn).all() and (nn>0).all() and np.all(nn==nn[:1]) and np.all(ref==ref[:1]),'incomplete grid or inconsistent reference'
        N=nn[0].sum(); nobs+=N; counts[b]={'clusters':n,'questions_or_tokens':float(N)};means+=x.sum(1)/N/H;refs+=ref.sum(1)/N/H;studs+=stu.sum(1)/N/H
        if n<2: taskvar=float('nan');continue
        d=x.mean(0);inf=d-d.sum()/N*nn[0];taskvar+=(n/(n-1))*(inf@inf)/N**2/H**2
    avg=means.mean();sd=means.std(ddof=1) if S>1 else float('nan');se=sd/math.sqrt(S);half=t.ppf(.975,S-1)*se if S>1 else float('nan')
    return {'ratio':ratio,'margin':margin,'seeds':S,'benchmark_counts':counts,'reference_score':float(refs.mean()),'student_score':float(studs.mean()),'observed_retention':float(studs.mean()/refs.mean()),'seed_scores':studs.tolist(),'contrast':float(avg),'fixed_suite_seed_sd':float(sd),'fixed_suite_seed_se':float(se),'fixed_suite_seed_t95':[float(avg-half),float(avg+half)],'fixed_models_cluster_se':float(math.sqrt(taskvar)),'planning_only_quadrature_se':float(math.sqrt(taskvar+se*se))}

def seed_power(sd,delta,s):
    if sd==0:return float(delta>0)
    return float(nct.sf(t.ppf(.975,s-1),s-1,delta*math.sqrt(s)/sd))

def main():
    a=argparse.ArgumentParser();a.add_argument('csv');a.add_argument('--ratio',type=float,default=.99);a.add_argument('--margin',type=float,default=0.);args=a.parse_args();print(json.dumps(audit(list(csv.DictReader(open(args.csv))),args.ratio,args.margin),indent=2))
if __name__=='__main__':main()
