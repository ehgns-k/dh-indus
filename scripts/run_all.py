"""Re-run every analysis script in dependency order and report which result
files changed (review R3). Usage: PYTHONPATH=src python scripts/run_all.py
Requires the raw data (scripts/fetch_*.py). The phonetic searches (phase7_e3*)
take tens of minutes."""
import subprocess, sys, time, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORDER = [
    "phase2_baseline.py", "phase1_concordance.py", "phase3_structure.py", "phase3_h33_heldout.py",
    "phase3_h34_sites.py", "phase3_h35_objecttype.py", "phase3_h35_explore_within_site.py", "phase3_h36_tabB.py",
    "phase3_h37_terminal_objecttype.py", "phase3_h38_strokes.py", "phase3_h39_strokes_heldout.py",
    "phase3_h310_stroke_followers.py", "phase3_h311_matched_control.py", "phase3_h312_count_item_pairs.py",
    "phase3_h313_fish_numerals.py", "phase4_h41_h42_claims.py", "phase4_h43_tablet_suffix.py",
    "phase4_h43_strict_control.py", "phase5_fresh_tests.py", "phase5_fresh_tests.py --set2",
    "phase6_c1_copper_motif.py", "phase3_numeral_table.py", "phase3_b1_b4_template_units.py",
    "phase5_h51_sign119.py", "phase5_h51b_sign002_fresh.py", "phase4_d1_typology.py", "phase4_d1_leave_one_out.py",
    "phase4_d2_nonlinguistic.py", "phase6_c2_association_scan.py", "phase6_f4_final_sign_fresh.py",
    "phase6_c2k_kp_typecodes.py", "phase6_c2k_code_meaning.py", "phase7_e2_sanskrit_readability.py",
    "phase7_e2b_random_assignments.py", "phase6_c3_penultimate_constructions.py", "review_r1_strict_heldout.py",
    "phase3_q2_sign_classes.py", "phase6_h61_numeral_series.py", "phase6_h61_without_033.py",
    "phase3_split_merge_strokes.py", "phase3_l3a_allographs.py", "phase3_l3a_allographs_10k.py",
    "phase3_l3b_allographs_kp.py", "phase3_l3b_allographs_kp_10k.py", "phase4_d3_inventory.py", "phase3_h71_hmm.py",
    "review_r2_h310_leave_one_out.py", "phase3_repetition.py", "phase4_d1_kp_robustness.py",
    "phase8_g1_shape_usage.py", "phase8_g2_close_shapes.py", "phase8_h81_abroad.py", "phase8_m1_marks.py",
    "phase8_g2_hog_robustness.py", "phase8_m1_hog_robustness.py", "phase9_h91_numeral_slot.py",
    "phase9_h91_count_differences.py", "phase9_h92_formula_objects.py", "phase9_h93_substitution_classes.py",
    "phase9_h94_classes_objects.py", "phase9_formulae.py", "phase10_t1_chronological_variants.py",
    "phase10_h101_site_specificity.py", "review_r4_h91_normalised_kp.py",
    "phase7_e3_phonetic_search.py", "phase7_e3b_corrected.py", "phase7_e3c_power.py", "phase7_e3d_equalised.py",
]
skip_heavy = "--skip-heavy" in sys.argv
failed = []
for item in ORDER:
    if skip_heavy and item.startswith("phase7_e3"):
        continue
    parts = item.split()
    t = time.time()
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / parts[0])] + parts[1:], cwd=ROOT,
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    print(f"{item:45s} {'ok' if r.returncode == 0 else 'FAILED'} {time.time() - t:6.1f}s", flush=True)
    if r.returncode:
        failed.append(item); print(r.stderr[-800:])
changed = subprocess.run(["git", "status", "--porcelain", "results", "docs/SIGN_CLASSES.md", "docs/FORMULAE.md"],
                         cwd=ROOT, capture_output=True, text=True).stdout
print("FAILED:", failed)
print("CHANGED RESULT FILES:\n" + (changed or "none"))
